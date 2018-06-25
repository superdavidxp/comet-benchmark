#!/usr/bin/env python

import os
import socket
import math
import random
import torch
import torchvision

class Partition(object):

   def __init__(self, data, index):
       self.data = data
       self.index = index

   def __len__(self):
       return len(self.index)
       data_idx = self.index[index]
       return self.data[data_idx]


class DataPartitioner(object):

   def __init__(self, data, sizes=[0.7, 0.2, 0.1], seed=1234):
       self.data = data
       self.partitions = []
       rng = random.Random()
       rng.seed(seed)
       data_len = len(data)
       indexes = [x for x in range(0, data_len)]
       rng.shuffle(indexes)

       for frac in sizes:
           part_len = int(frac * data_len)
           self.partitions.append(indexes[0:part_len])
           indexes = indexes[part_len:]

   def use(self, partition):
       return Partition(self.data, self.partitions[partition])

class Net(torch.nn.Module):
   def __init__(self):
       super(Net, self).__init__()
       self.conv1 = torch.nn.Conv2d(1, 10, kernel_size=5)
       self.conv2 = torch.nn.Conv2d(10, 20, kernel_size=5)
       self.conv2_drop = torch.nn.Dropout2d()
       self.fc1 = torch.nn.Linear(320, 50)
       self.fc2 = torch.nn.Linear(50, 10)

   def forward(self, x):
       x = torch.nn.functional.relu(torch.nn.functional.max_pool2d(self.conv1(x), 2))
       x = torch.nn.functional.relu(torch.nn.functional.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
       x = x.view(-1, 320)
       x = torch.nn.functional.relu(self.fc1(x))
       x = torch.nn.functional.dropout(x, training=self.training)
       x = self.fc2(x)
       return torch.nn.functional.log_softmax(x, dim=1)

def partition_dataset():
   size = torch.distributed.get_world_size()
   bsz = 128 / float(size)
   partition_sizes = [1.0 / size for _ in range(size)]
   partition = DataPartitioner(dataset, partition_sizes)
   partition = partition.use(torch.distributed.get_rank())
   train_set = torch.utils.data.DataLoader(partition, batch_size=bsz, shuffle=True)
   return train_set, bsz


def average_gradients(model):
   size = float(torch.distributed.get_world_size())
   for param in model.parameters():
       torch.distributed.all_reduce(param.grad.data, op=torch.distributed.reduce_op.SUM)
       param.grad.data /= size


def run(rank, size):
   hostname = socket.gethostname()
   torch.manual_seed(1234)
   train_set, bsz = partition_dataset()
   model = Net()
   optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.5)

   num_batches = math.ceil(len(train_set.dataset) / float(bsz))
   for epoch in range(10):
       epoch_loss = 0.0
       for data, target in train_set:
           data, target = torch.autograd.Variable(data), torch.autograd.Variable(target)
           optimizer.zero_grad()
           output = model(data)
           loss = torch.nn.functional.nll_loss(output, target)
           epoch_loss += loss.data[0]
           loss.backward()
           average_gradients(model)
           optimizer.step()

       print('Rank ', torch.distributed.get_rank(), ' on ', hostname, ' at epoch ', epoch, ': ', epoch_loss / num_batches)

if __name__ == "__main__":

   slurmjobid = os.environ['SLURM_JOB_ID']
   ntasks = int(os.environ['SLURM_NTASKS'])
   rank_id = int(os.environ['SLURM_PROCID'])

   torch.distributed.init_process_group(backend='gloo', init_method='file:///home/dmu/nodelist.o' + slurmjobid, rank=rank_id, world_size=ntasks)

   run(rank_id, ntasks)
