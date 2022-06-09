#!/bin/bash

# Recreate config file
rm -rf /app/client/build/_snowpack/env.js
touch /app/client/build/_snowpack/env.js

# Add assignment
echo "export const MODE = 'production';
export const NODE_ENV = 'production';
export const SSR = false;" >> /app/client/build/_snowpack/env.js

# Read each line in .env file
# Each line represents key=value pairs
while read -r line || [[ -n "$line" ]];
do
  # Split env variables by character `=`
  if printf '%s\n' "$line" | grep -q -e '='; then
    varname=$(printf '%s\n' "$line" | sed -e 's/=.*//')
    varvalue=$(printf '%s\n' "$line" | sed -e 's/^[^=]*=//')
  fi

  # Read value of current variable if exists as Environment variable
  value=$(printf '%s\n' "${!varname}")
  # Otherwise use value from .env file
  [[ -z $value ]] && value=${varvalue}

  # Append configuration property to JS file
  echo "export const $varname = \"$value\";" >> /app/client/build/_snowpack/env.js
done < /app/client/.env

echo "" >> /app/client/build/_snowpack/env.js
