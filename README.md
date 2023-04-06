# proxyServerForStableDiffusion

## Usage
### 1. Modify local_config.py file


### 2. Build docker image
```bash
sudo docker build --tag proxyserver .
```

### 3. Run proxyserver
```bash
sudo docker run -d --restart always -p 5000:5000 proxyserver 
```