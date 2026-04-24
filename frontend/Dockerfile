# przypinamy konkretną wersję
FROM nginx:1.27-alpine

# # usuwamy domyślną stronę startową Nginxa
# RUN rm -rf /usr/share/nginx/html/*
# 
# # kopiujemy statyki i konfigurację
# COPY html/ /usr/share/nginx/html/
# COPY nginx.conf /etc/nginx/nginx.conf

# usuń domyślną stronę startową Nginxa
RUN rm -rf /usr/share/nginx/html/*

# kopiuj skrypt startowy
COPY docker-entrypoint.sh /docker-entrypoint.d/40-envsubst-html.sh
RUN chmod +x /docker-entrypoint.d/40-envsubst-html.sh

# kopiuj konfigurację
COPY nginx.conf /etc/nginx/nginx.conf

# kopiuj szablon HTML (z ${MOJA_ZMIENNA} w środku)
COPY index.html.template /usr/share/nginx/html/index.html.template

