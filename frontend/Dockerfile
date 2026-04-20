# przypinamy konkretną wersję
FROM nginx:1.27-alpine

# usuwamy domyślną stronę startową Nginxa
RUN rm -rf /usr/share/nginx/html/*

# kopiujemy statyki i konfigurację
COPY html/ /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/nginx.conf
