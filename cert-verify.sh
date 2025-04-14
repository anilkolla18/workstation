#!/bin/bash

DAYS_THRESHOLD=90
SOON_THRESHOLD=30
NOW=$(date +%s)

echo "Kubernetes TLS Certificate Expiry Report"
echo "Generated on: $(date)"
echo "========================================"

# Temporary file to store output
temp_output=$(mktemp)

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

    # Handle expired certificates
    if [ "$days_left" -lt 0 ]; then
      echo "❌ $secret - EXPIRED (expired on $expiration)" >> "$temp_output"
    elif [ "$days_left" -le "$SOON_THRESHOLD" ]; then
      echo "🚨 $secret - EXPIRES IN ${days_left} days (on $expiration)" >> "$temp_output"
    elif [ "$days_left" -le "$DAYS_THRESHOLD" ]; then
      echo "⚠️  $secret - Expires in ${days_left} days (on $expiration)" >> "$temp_output"
    else
      echo "✅ $secret - Valid for ${days_left} more days (expires on $expiration)" >> "$temp_output"
    fi
  fi
done

# Sort by the number of days left (ascending order)
sort -t' ' -k6,6n "$temp_output"

# Clean up temporary file
rm "$temp_output"
