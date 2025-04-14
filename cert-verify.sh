#!/bin/bash

DAYS_THRESHOLD=90
SOON_THRESHOLD=30
NOW=$(date +%s)

echo "Kubernetes TLS Certificate Expiry Report"
echo "Generated on: $(date)"
echo "========================================"

for secret in $(kubectl get secrets -o jsonpath='{.items[*].metadata.name}'); do
  if kubectl get secret "$secret" -o jsonpath='{.data}' | grep -q 'tls.crt'; then
    cert_data=$(kubectl get secret "$secret" -o jsonpath='{.data.tls\.crt}' | base64 -d 2>/dev/null)

    if [ -z "$cert_data" ]; then
      continue
    fi

    expiration=$(openssl x509 -noout -enddate -in <(echo "$cert_data") 2>/dev/null | cut -d= -f2)

    if [ -z "$expiration" ]; then
      continue
    fi

    expiration_epoch=$(date -d "$expiration" +%s)
    days_left=$(( (expiration_epoch - NOW) / 86400 ))

    if [ "$days_left" -le "$SOON_THRESHOLD" ]; then
      echo "🚨 $secret - EXPIRES IN $days_left DAYS on $expiration"
    elif [ "$days_left" -le "$DAYS_THRESHOLD" ]; then
      echo "⚠️  $secret - expires in $days_left days on $expiration"
    else
      echo "✅ $secret - expires in $days_left days on $expiration"
    fi
  fi
done
