isort esite &&
  autoflake -r --in-place --remove-all-unused-imports --remove-unused-variables esite &&
  black esite
