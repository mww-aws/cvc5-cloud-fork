################### Build Mallob
FROM satcomp-common-base-image
USER root
#  Install required softwares
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt install -y cmake build-essential zlib1g-dev libopenmpi-dev wget unzip build-essential zlib1g-dev cmake python3 build-essential gfortran wget curl

# Build Mallob
RUN git clone https://github.com/cvc5/cvc5.git
WORKDIR cvc5
RUN ./configure --auto-download
RUN cd build && make && cd ..