#!/bin/sh

echo "Install CMU pocketsphinx sphinx"

sudo rm -rf pocketsphinx*
sudo rm -rf sphinxbase*

wget -O sphinxbase.zip https://github.com/cmusphinx/sphinxbase/archive/master.zip
unzip sphinxbase.zip
cd sphinxbase-master
sh /srv/speechy_env/bin/activate && ./autogen.sh
make
sudo make install

cd ../

wget -O pocketsphinx.zip https://github.com/cmusphinx/pocketsphinx/archive/master.zip
unzip pocketsphinx.zip
cd pocketsphinx-master
sh /srv/speechy_env/bin/activate && ./autogen.sh
make
sudo make install



