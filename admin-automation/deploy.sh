#!/usr/bin/env bash
set -euo pipefail

# ─── LOAD LOCAL .env ─────────────────────────────────────────────────────────
if [ -f .env ]; then
  echo "🔒 loading .env"
  set -o allexport
  source .env
  set +o allexport
else
  echo "❌ .env not found – please create it with required vars" >&2
  exit 1
fi

# ─── ENSURE MANDATORY ENV VARS ────────────────────────────────────────────────
for var in AWS_PROFILE REGION SSM_PATH STACK_NAME; do
  if [ -z "${!var-}" ]; then
    echo "❌ Missing env‐var: $var" >&2
    exit 1
  fi
done

# ─── LIST OF PARAMS TO PUBLISH ────────────────────────────────────────────────
PARAMS=(
  GMAIL_APP_PASSWORD
  JIRA_SERVER
  JIRA_USER
  JIRA_API_TOKEN
  PRIMARY_GMAIL_SENDER_ADDRESS
  SECONDARY_GMAIL_SENDER_ADDRESS
  BUDDY_PROGRAM_VENDOR_ADDRESSES
  COORDINADORA_USER
  COORDINADORA_PASSWORD
  COORDINADORA_API
  COORDINADORA_USER_ID
  SLACK_BOT_TOKEN
  SLACK_OB_CHANNEL_ID
  BAMBOOHR_SUBDOMAIN
  BAMBOOHR_API_KEY
)

echo
echo "🟢 Pushing parameters to SSM at '${SSM_PATH}' in ${REGION}/${AWS_PROFILE}…"
for NAME in "${PARAMS[@]}"; do
  VALUE="${!NAME-}"
  if [ -z "$VALUE" ]; then
    echo "❌ Missing env‐var: $NAME" >&2
    exit 1
  fi

  PARAM_NAME="${SSM_PATH}/${NAME}"
  echo " • $PARAM_NAME"

  # write the literal value to a temp file
  TMPFILE=$(mktemp)
  printf '%s' "$VALUE" > "$TMPFILE"

  # use file:// to force CLI to read the local file contents
  aws ssm put-parameter \
    --name      "$PARAM_NAME" \
    --type      String \
    --value     "file://$TMPFILE" \
    --overwrite \
    --profile   "$AWS_PROFILE" \
    --region    "$REGION"

  rm -f "$TMPFILE"
done

# ─── BUILD & DEPLOY THE SAM APP ───────────────────────────────────────────────
echo
echo "🛠  Building SAM application…"
sam build

echo
echo "🚀 Deploying SAM stack '$STACK_NAME'…"
sam deploy \
  --stack-name           "$STACK_NAME" \
  --region               "$REGION" \
  --profile              "$AWS_PROFILE" \
  --capabilities         CAPABILITY_IAM \
  --no-confirm-changeset \
  --no-fail-on-empty-changeset

echo
echo "✅ All done! SSM parameters updated and SAM stack '$STACK_NAME' deployed."
