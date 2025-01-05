# syntax=docker/dockerfile:1

FROM node:12-buster AS wwwstage

ARG KASMWEB_RELEASE="46412d23aff1f45dffa83fafb04a683282c8db58"

RUN \
  echo "**** build clientside ****" && \
  export QT_QPA_PLATFORM=offscreen && \
  export QT_QPA_FONTDIR=/usr/share/fonts && \
  mkdir /src && \
  cd /src && \
  wget https://github.com/kasmtech/noVNC/tarball/${KASMWEB_RELEASE} -O - \
    | tar  --strip-components=1 -xz && \
  npm install && \
  npm run-script build

RUN \
  echo "**** organize output ****" && \
  mkdir /build-out && \
  cd /src && \
  rm -rf node_modules/ && \
  cp -R ./* /build-out/ && \
  cd /build-out && \
  rm *.md && \
  rm AUTHORS && \
  cp index.html vnc.html && \
  mkdir Downloads


FROM ghcr.io/linuxserver/baseimage-ubuntu:jammy AS buildstage

ARG KASMVNC_RELEASE="0ebbbc6412e131092308cc1ce10b9d106e3b4e05"

COPY --from=wwwstage /build-out /www

RUN \
  echo "**** install build deps ****" && \
  apt-get update && \
  apt-get build-dep -y \
    libxfont-dev \
    xorg-server && \
  apt-get install -y \
    autoconf \
    automake \
    cmake \
    git \
    grep \
    libavcodec-dev \
    libdrm-dev \
    libepoxy-dev \
    libgbm-dev \
    libgif-dev \
    libgnutls28-dev \
    libgnutls28-dev \
    libjpeg-dev \
    libjpeg-turbo8-dev \
    libpciaccess-dev \
    libpng-dev \
    libssl-dev \
    libtiff-dev \
    libtool \
    libwebp-dev \
    libx11-dev \
    libxau-dev \
    libxcursor-dev \
    libxcursor-dev \
    libxcvt-dev \
    libxdmcp-dev \
    libxext-dev \
    libxkbfile-dev \
    libxrandr-dev \
    libxrandr-dev \
    libxshmfence-dev \
    libxtst-dev \
    meson \
    nettle-dev \
    tar \
    tightvncserver \
    wget \
    wayland-protocols \
    xinit \
    xserver-xorg-dev

RUN \
  echo "**** build libjpeg-turbo ****" && \
  mkdir /jpeg-turbo && \
  JPEG_TURBO_RELEASE=$(curl -sX GET "https://api.github.com/repos/libjpeg-turbo/libjpeg-turbo/releases/latest" \
  | awk '/tag_name/{print $4;exit}' FS='[""]'); \
  curl -o \
  /tmp/jpeg-turbo.tar.gz -L \
    "https://github.com/libjpeg-turbo/libjpeg-turbo/archive/${JPEG_TURBO_RELEASE}.tar.gz" && \
  tar xf \
  /tmp/jpeg-turbo.tar.gz -C \
    /jpeg-turbo/ --strip-components=1 && \
  cd /jpeg-turbo && \
  MAKEFLAGS=-j`nproc` \
  CFLAGS="-fpic" \
  cmake -DCMAKE_INSTALL_PREFIX=/usr/local -G"Unix Makefiles" && \
  make && \
  make install

RUN \
  echo "**** build kasmvnc ****" && \
  git clone https://github.com/kasmtech/KasmVNC.git src && \
  cd /src && \
  git checkout -f ${KASMVNC_release} && \
  sed -i \
    -e '/find_package(FLTK/s@^@#@' \
    -e '/add_subdirectory(tests/s@^@#@' \
    CMakeLists.txt && \
  cmake \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DBUILD_VIEWER:BOOL=OFF \
    -DENABLE_GNUTLS:BOOL=OFF \
    . && \
  make -j4 && \
  echo "**** build xorg ****" && \
  XORG_VER="21.1.4" && \
  wget --no-check-certificate \
    -O /tmp/xorg-server-${XORG_VER}.tar.gz \
    "https://www.x.org/archive/individual/xserver/xorg-server-${XORG_VER}.tar.gz" && \
  tar --strip-components=1 \
    -C unix/xserver \
    -xf /tmp/xorg-server-${XORG_VER}.tar.gz && \
  cd unix/xserver && \
  patch -Np1 -i ../xserver21.patch && \
  patch -s -p0 < ../CVE-2022-2320-v1.20.patch && \
  autoreconf -i && \
  ./configure --prefix=/opt/kasmweb \
    --with-xkb-path=/usr/share/X11/xkb \
    --with-xkb-output=/var/lib/xkb \
    --with-xkb-bin-directory=/usr/bin \
    --with-default-font-path="/usr/share/fonts/X11/misc,/usr/share/fonts/X11/cyrillic,/usr/share/fonts/X11/100dpi/:unscaled,/usr/share/fonts/X11/75dpi/:unscaled,/usr/share/fonts/X11/Type1,/usr/share/fonts/X11/100dpi,/usr/share/fonts/X11/75dpi,built-ins" \
    --with-sha1=libcrypto \
    --without-dtrace --disable-dri \
    --disable-static \
    --disable-xinerama \
    --disable-xvfb \
    --disable-xnest \
    --disable-xorg \
    --disable-dmx \
    --disable-xwin \
    --disable-xephyr \
    --disable-kdrive \
    --disable-config-hal \
    --disable-config-udev \
    --disable-dri2 \
    --enable-glx \
    --disable-xwayland \
    --enable-dri3 && \
  find . -name "Makefile" -exec sed -i 's/-Werror=array-bounds//g' {} \; && \
  make -j4

RUN \
  echo "**** generate final output ****" && \
  cd /src && \
  mkdir -p xorg.build/bin && \
  cd xorg.build/bin/ && \
  ln -s /src/unix/xserver/hw/vnc/Xvnc Xvnc && \
  cd .. && \
  mkdir -p man/man1 && \
  touch man/man1/Xserver.1 && \
  cp /src/unix/xserver/hw/vnc/Xvnc.man man/man1/Xvnc.1 && \
  mkdir lib && \
  cd lib && \
  ln -s /usr/lib/x86_64-linux-gnu/dri dri && \
  cd /src && \
  mkdir -p builder/www && \
  cp -ax /www/* builder/www/ && \
  cp builder/www/index.html builder/www/vnc.html && \
  make servertarball && \
  mkdir /build-out && \
  tar xzf \
    kasmvnc-Linux*.tar.gz \
    -C /build-out/ && \
  rm -Rf /build-out/usr/local/man

# nodejs builder
FROM ghcr.io/linuxserver/baseimage-ubuntu:jammy AS nodebuilder
ARG KCLIENT_RELEASE

RUN \
  echo "**** install build deps ****" && \
  apt-get update && \
  apt-get install -y \
    gnupg && \
  curl -s https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - && \
  echo 'deb https://deb.nodesource.com/node_18.x jammy main' \
    > /etc/apt/sources.list.d/nodesource.list && \
  apt-get update && \
  apt-get install -y \
    g++ \
    gcc \
    libpam0g-dev \
    libpulse-dev \
    make \
    nodejs
	
RUN \
  echo "**** grab source ****" && \
  mkdir -p /kclient && \
  if [ -z ${KCLIENT_RELEASE+x} ]; then \
    KCLIENT_RELEASE=$(curl -sX GET "https://api.github.com/repos/linuxserver/kclient/releases/latest" \
    | awk '/tag_name/{print $4;exit}' FS='[""]'); \
  fi && \
  curl -o \
  /tmp/kclient.tar.gz -L \
    "https://github.com/linuxserver/kclient/archive/${KCLIENT_RELEASE}.tar.gz" && \
  tar xf \
  /tmp/kclient.tar.gz -C \
    /kclient/ --strip-components=1

RUN \
  echo "**** install node modules ****" && \
  cd /kclient && \
  npm install && \
  rm -f package-lock.json

# runtime stage
FROM nestybox/ubuntu-jammy-systemd-docker:latest

# copy over build output
COPY --from=nodebuilder /kclient /kclient
COPY --from=buildstage /build-out/ /

RUN echo "**** Install needed software ********" && \
  apt-get update && \
  apt-get upgrade -y && \
  apt-get install -y \
    apt-utils \
    locales \
    catatonit \
    cron \
    curl \
    gnupg \
    jq \
    netcat \
    tzdata
RUN echo "**** generate locale ****" && \
  locale-gen en_US.UTF-8 && \
  echo "**** enable locales ****" && \
  sed -i \
    '/locale/d' \
    /etc/dpkg/dpkg.cfg.d/excludes
RUN echo "**** install deps ****" && \
  curl -s https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - && \
  echo 'deb https://deb.nodesource.com/node_18.x jammy main' \
    > /etc/apt/sources.list.d/nodesource.list && \
  apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
    ca-certificates \
    dbus-x11 \
    dunst \
    ffmpeg \
    file \
    fonts-noto-color-emoji \
    fonts-noto-core \
    fuse-overlayfs \
    intel-media-va-driver \
    libdatetime-perl \
    libfontenc1 \
    libfreetype6 \
    libgbm1 \
    libgcrypt20 \
    libgl1-mesa-dri \
    libglu1-mesa \
    libgnutls30 \
    libgomp1 \
    libhash-merge-simple-perl \
    libjpeg-turbo8 \
    libnotify-bin \
    liblist-moreutils-perl \
    libp11-kit0 \
    libpam0g \
    libpixman-1-0 \
    libscalar-list-utils-perl \
    libswitch-perl \
    libtasn1-6 \
    libtry-tiny-perl \
    libvulkan1 \
    libwebp7 \
    libx11-6 \
    libxau6 \
    libxcb1 \
    libxcursor1 \
    libxdmcp6 \
    libxext6 \
    libxfixes3 \
    libxfont2 \
    libxinerama1 \
    libxshmfence1 \
    libxtst6 \
    libyaml-tiny-perl \
    locales-all \
    mesa-va-drivers \
    mesa-vulkan-drivers \
    nginx \
    nodejs \
    openssh-client \
    openssl \
    pciutils \
    perl \
    procps \
    pulseaudio \
    pulseaudio-utils \
    python3 \
    software-properties-common \
    ssl-cert \
    sudo \
    tar \
    util-linux \
    x11-apps \
    x11-common \
    x11-utils \
    x11-xkb-utils \
    x11-xkb-utils \
    x11-xserver-utils \
    xauth \
    xdg-utils \
    xfonts-base \
    xkb-data \
    xserver-common \
    xserver-xorg-core \
    xserver-xorg-video-amdgpu \
    xserver-xorg-video-ati \
    xserver-xorg-video-intel \
    xserver-xorg-video-nouveau \
    xserver-xorg-video-qxl \
    xterm \
    xutils \
    zlib1g \
    mousepad \
    xfce4-terminal \
    xfce4 \
    xubuntu-default-settings \
    xubuntu-icon-theme
RUN echo "**** filesystem setup ****" && \
    ln -s /usr/local/share/kasmvnc /usr/share/kasmvnc && \
    ln -s /usr/local/etc/kasmvnc /etc/kasmvnc && \
    ln -s /usr/local/lib/kasmvnc /usr/lib/kasmvncserver && \
    echo "**** user perms ****" && \
    sed -e 's/%sudo	ALL=(ALL:ALL) ALL/%sudo ALL=(ALL:ALL) NOPASSWD: ALL/g' \
      -i /etc/sudoers && \
    echo "**** proot-apps ****" && \
    mkdir /proot-apps/ && \
    PAPPS_RELEASE=$(curl -sX GET "https://api.github.com/repos/linuxserver/proot-apps/releases/latest" \
      | awk '/tag_name/{print $4;exit}' FS='[""]') && \
    curl -L https://github.com/linuxserver/proot-apps/releases/download/${PAPPS_RELEASE}/proot-apps-x86_64.tar.gz \
      | tar -xzf - -C /proot-apps/ && \
    echo "${PAPPS_RELEASE}" > /proot-apps/pversion && \
    echo "**** locales ****" && \
    for LOCALE in $(curl -sL https://raw.githubusercontent.com/thelamer/lang-stash/master/langs); do \
      localedef -i $LOCALE -f UTF-8 $LOCALE.UTF-8; \
    done && \
    echo "**** xfce tweaks ****" && \
      rm -f /etc/xdg/autostart/xscreensaver.desktop

ENV TERM="xterm"
ENV DISPLAY=:1

COPY /root /

# ports and volumes
EXPOSE 3000

ENTRYPOINT [ "/sbin/init" ]
