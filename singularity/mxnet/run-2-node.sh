./launch.py -n 2 -H hosts --launcher ssh python image_classification.py --dataset cifar10 --model vgg11 --epochs 1 --kvstore dist_sync
