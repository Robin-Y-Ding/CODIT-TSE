CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
FORMATTED_DIR=$CURRENT_DIR/FormattedBuggyFiles
echo "Creating directory 'FormattedBuggyFiles'"
mkdir -p $FORMATTED_DIR
echo

echo "Reading from d4jPath.txt"
while IFS=' ' read -r col1 col2
do
  BUGID="$(cut -d'/' -f9 <<<"$col1")"
  BN=$( basename $col1)
  java -jar ../ReformatJavaFile.jar $col1 > $FORMATTED_DIR/$BUGID'_'$BN
done < d4jPath.txt
