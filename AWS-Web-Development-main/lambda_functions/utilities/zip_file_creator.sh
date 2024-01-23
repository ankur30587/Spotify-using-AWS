zip_files=(
  "add_subscription.zip:add_subscription.py:requirements.txt"
  "retrieve_user.zip:retrieve_user.py:requirements.txt"
  "add_user.zip:add_user.py:requirements.txt"
  "all_songs.zip:all_songs.py:requirements.txt"
  "delete_subscription.zip:delete_subscription.py:requirements.txt"
  "unsubscribed.zip:unsubscribed.py:requirements.txt"
  "user_subscription.zip:user_subscription.py:requirements.txt"
)

for file in "${zip_files[@]}"; do
  arr=(${file//:/ })
  zip_file=${arr[0]}
  python_file=${arr[1]}
  requirements_file=${arr[2]}

  # Check if the Python file exists
  if [ ! -f "$python_file" ]; then
    echo "$python_file does not exist"
    continue
  fi

  # Check if the requirements file exists
  if [ ! -f "$requirements_file" ]; then
    echo "$requirements_file does not exist"
    continue
  fi

  # Create the ZIP archive
  zip -r "$zip_file" "$python_file" "$requirements_file"

  # Check if the ZIP archive was created successfully
  if [ $? -eq 0 ]; then
    echo "$zip_file created successfully"
  else
    echo "Failed to create $zip_file"
  fi
done
