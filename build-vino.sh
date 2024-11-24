# Edited by ANG 24.11.19
# sudo apt install libtbb-dev libjpeg-dev libtiff-dev libwebp-dev
# mkdir opencv-4.5.2-openvino/build
# conda activate torch
cd opencv-4.5.2-openvino/build
cmake \    
     -DCMAKE_INSTALL_PREFIX=/opt/intel/openvino/opencv \    
     -DCMAKE_BUILD_TYPE=Release \    
     -DWITH_INF_ENGINE=ON \    
     -DENABLE_CXX11=ON \    
     -DWITH_TBB=ON \    
     -DPYTHON_EXECUTABLE=~/miniconda3/envs/torch/bin/python \   
     -DPYTHON_LIBRARY=$(python3 -c "import distutils.sysconfig as sysconfig; print(sysconfig.get_config_var('LIBDIR'))") \    
     -DPYTHON_INCLUDE_DIR=$(python3 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") .
make -j 4
sudo make install
