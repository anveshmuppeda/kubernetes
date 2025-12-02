# Gateway API

helm install traefik traefik/traefik \
  --version $CHART_VERSION \
  --values traefik/values.yaml \
  --namespace traefik \
  --create-namespace