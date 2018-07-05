# theano

We need to create a file named ".theanorc" under $HOME (~) directory.

1. Paste following script to use GPU 
```
[global]  
device = cuda  
floatX = float32
```

2. Paste following script to use CPU 
```
[global]  
device = cpu  
floatX = float32
```
