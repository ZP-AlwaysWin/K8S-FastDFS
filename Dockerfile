FROM centos

MAINTAINER zhangp "www.AlwaysWin.com"
ENV NGINX_VERSION 1.10.3
ENV OPENSSL_VERSION 1.0.2k
ENV PCRE_VERSION 8.40
ENV ZLIB_VERSION 1.2.11
ENV BUILD_ROOT /usr/local/src/nginx

# 为了减小最终生成的镜像占用的空间，这里没有执行yum update命令，可能不是好的实践
# 为了加快构建速度，这里使用了163的安装源
#RUN yum -y update \
ADD  ngx_cache_purge-2.3.tar.gz /tmp
RUN     yum -y install curl \
        && mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup \
        && curl http://mirrors.163.com/.help/CentOS7-Base-163.repo -o /etc/yum.repos.d/CentOS7-Base-163.repo \ 
        && yum clean all \
        && yum makecache \
        && yum -y install gcc gcc-c++ make perl zip unzip \
        && mkdir -p $BUILD_ROOT \
        && cd $BUILD_ROOT \
        && curl https://ftp.pcre.org/pub/pcre/pcre-$PCRE_VERSION.zip -o $BUILD_ROOT/pcre-$PCRE_VERSION.zip \
        && curl https://www.openssl.org/source/openssl-$OPENSSL_VERSION.tar.gz -o $BUILD_ROOT/openssl-$OPENSSL_VERSION.tar.gz \
        && curl http://www.zlib.net/zlib-$ZLIB_VERSION.tar.gz -o $BUILD_ROOT/zlib-$ZLIB_VERSION.tar.gz \
        && curl https://nginx.org/download/nginx-$NGINX_VERSION.tar.gz -o $BUILD_ROOT/nginx-$NGINX_VERSION.tar.gz \
        && tar vxzf nginx-$NGINX_VERSION.tar.gz \
        && unzip pcre-$PCRE_VERSION.zip \
        && tar vxfz zlib-$ZLIB_VERSION.tar.gz \
        && tar vxfz openssl-$OPENSSL_VERSION.tar.gz \
        && cd nginx-$NGINX_VERSION \
        && BUILD_CONFIG="\
            --prefix=/etc/nginx \
            --sbin-path=/usr/sbin/nginx \
            --conf-path=/etc/nginx/nginx.conf \
            --error-log-path=/var/log/nginx/error.log \
            --http-log-path=/var/log/nginx/access.log \
            --pid-path=/var/run/nginx.pid \
            --lock-path=/var/run/nginx.lock \
            --http-client-body-temp-path=/var/cache/nginx/client_temp \
            --http-proxy-temp-path=/var/cache/nginx/proxy_temp \
            --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp \
            --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp \
            --http-scgi-temp-path=/var/cache/nginx/scgi_temp \
            --with-openssl=$BUILD_ROOT/openssl-$OPENSSL_VERSION \
            --with-pcre=$BUILD_ROOT/pcre-$PCRE_VERSION \
            --with-zlib=$BUILD_ROOT/zlib-$ZLIB_VERSION \
            --with-http_ssl_module \
            --with-http_v2_module \ 
            --with-threads \
            --add-module=/tmp/ngx_cache_purge-2.3 \
            " \
        && mkdir -p /var/cache/nginx \
        && ./configure $BUILD_CONFIG \
        && make && make install \
        && rm -rf $BUILD_ROOT \
        && yum -y remove gcc gcc-c++ make perl zip unzip \
        && yum clean all \
        && rm -rf /var/cache/yum \
        && rm -rf /tmp/* \
USER root
EXPOSE 80 443
CMD ["nginx", "-g", "daemon off;"]
