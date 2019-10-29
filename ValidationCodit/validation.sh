CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
DEFECTS4J_DIR=$CURRENT_DIR/Defects4J_projects
echo "Creating directory 'Defects4J_projects'"
mkdir -p $DEFECTS4J_DIR
echo

echo "Reading from Defects4J_oneLiner_metadata.csv"
while IFS=, read -r col1 col2 col3 col4
do
  BUG_PROJECT=${DEFECTS4J_DIR}/${col1}_${col2}
  mkdir -p $BUG_PROJECT
  echo "Checking out ${col1}_${col2} to ${BUG_PROJECT}"
  defects4j checkout -p $col1 -v ${col2}b -w $BUG_PROJECT &>/dev/null
  echo

  echo "Running test on all patches for ${col1}_${col2}"
  python3 ./ValidatePatch.py ./Patches/${col1}_${col2}/ $BUG_PROJECT ${DEFECTS4J_DIR}/
  echo

  echo "Deleting ${BUG_PROJECT}"
  rm -rf $BUG_PROJECT
  echo
done < Defects4J_oneLiner_metadata.csv

echo "Deleting Defects4J_projects"
rm -rf $DEFECTS4J_DIR
echo