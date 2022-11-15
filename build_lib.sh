# build shared libwhisper.so
git clone https://github.com/ggerganov/whisper.cpp /tmp/whispercpp
cd /tmp/whispercpp
# last commit before a breaking change
git checkout d6b84b2a23220dd8b8792872a3ab6802cd24b424
gcc -O3 -std=c11   -pthread -mavx -mavx2 -mfma -mf16c -fPIC -c ggml.c
g++ -O3 -std=c++11 -pthread --shared -fPIC -static-libstdc++ whisper.cpp ggml.o -o libwhisper.so
cp libwhisper.so $HOME/.local/bin/libwhisper.so