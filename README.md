<!-- LTeX: language=pl-PL -->

# Wdrożenie `k8s-test-app` do klastra `k3s`

Ten katalog zawiera manifest Kubernetes dla aplikacji `k8s-test-app` (frontend + backend) uruchamianej w klastrze opisanym w dokumentach 01-07.

Plik manifestu:

- `manifest/manifest.yaml`

## Co wdraża manifest

Manifest tworzy:

- Namespace `k8s-test-app`
- Deployment + Service dla backendu (Flask, port 5000)
- Deployment + Service dla frontendu (Nginx, port 80)
- Ingress dla Traefik z routingiem:
  - `/api` -> backend
  - `/` -> frontend

## Wymagania

Przed wdrożeniem upewnij się, ze:

- masz dostęp do klastra przez `kubeconfig` (np. `~/.kube/sec06.yaml`),
- w klastrze działa Traefik (`ingressClassName: traefik`),
- obrazy są opublikowane w GHCR:
  - `ghcr.io/mickeyreg/k8s_test_app-backend:latest`
  - `ghcr.io/mickeyreg/k8s_test_app-frontend:latest`

Zaktualizuj pola image w `mainifest/manifest.yaml` tak, aby pobierane były obrazy z Twojego użytkownika.

## Wdrożenie

Uruchom z katalogu student:

```bash
kubectl --kubeconfig ~/.kube/sec06.yaml apply -f manifest/manifest.yaml
```

## Weryfikacja

```bash
kubectl --kubeconfig ~/.kube/sec06.yaml get pods -n k8s-test-app
kubectl --kubeconfig ~/.kube/sec06.yaml get svc -n k8s-test-app
kubectl --kubeconfig ~/.kube/sec06.yaml get ingress -n k8s-test-app
```

Sprawdzenie szczegółów:

```bash
kubectl --kubeconfig ~/.kube/sec06.yaml describe ingress k8s-test-app -n k8s-test-app
kubectl --kubeconfig ~/.kube/sec06.yaml logs deploy/backend -n k8s-test-app
```

## Dostep do aplikacji

Węzeł zdefiniowany w manifeście:

- `k8s_test_app.10.10.16.101.nip.io`

Po poprawnym wdrożeniu i działającym Ingress aplikacja powinna być dostępna pod adresem HTTP:

- `http://k8s_test_app.10.10.16.101.nip.io`.

## Aktualizacja wersji aplikacji

Aktualizacja opiera się na zmianie tagu obrazu w `manifest/manifest.yaml` i ponownym jego wdrożeniu za pomocą komendy `apply`.

Przyklad:

- `ghcr.io/mickeyreg/k8s_test_app-backend:sha-...`
- `ghcr.io/mickeyreg/k8s_test_app-frontend:sha-...`

Następnie:

```bash
kubectl --kubeconfig ~/.kube/sec06.yaml apply -f manifest/manifest.yaml
```
