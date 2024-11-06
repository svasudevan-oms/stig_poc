usage="$(basename "$0") [-c] [-h] [-i hostsfile] username [address]"
function error {
  echo "$usage"
  exit 1
}
hostsfile="hosts"
check=false
while getopts ":chi:" opt; do
  case $opt in
    c)
      check=true
      shift
      ;;
    h)
      error
      ;;
    i)
      hostsfile="$OPTARG"
      shift 2
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      error
      ;;
  esac
done
if [ -z "$1" ]; then
  echo "Missing required username"
  error
fi
echo "Using hosts file "$hostsfile""
if [ -n "$2" ]; then
  host=""$2" ansible_connection=network_cli ansible_network_os=ios ansible_become=yes ansible_become_method=enable"
  echo "To be written: "$host""
  if [ -f "$hostsfile" ]; then
    echo "Overwrite "$hostsfile" file?"
    select yn in "Yes" "No"; do
      case "$yn,$REPLY" in
        Yes,*|*,[Yy]es|*,[Yy])
          echo "$host" > "$hostsfile"
          break
          ;;
        No,*|*,[Nn]o|*,[Nn])
          echo "Using $hostsfile without overwrite."
          break
          ;;
      esac
    done
  else
    echo "$host" > "$hostsfile"
  fi
fi
echo "Logging in as "$1""
if [ "$check" = false ]; then
  ansible-playbook -v -u "$1" -k -K -i "$hostsfile" site.yml
else
  echo "Running in check-only mode..."
  ansible-playbook -v -C -e "ignore_all_errors=True" -u "$1" -k -K -i "$hostsfile" site.yml
fi
