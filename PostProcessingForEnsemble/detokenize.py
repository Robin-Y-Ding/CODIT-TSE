import sys
import glob
import re
import os

def ProcessPredictions(pre_fix):
    text_files = pre_fix + '*.txt'
    fn_list = glob.glob(text_files)

    for fn in fn_list:
        file_path = fn.replace("\\", '/')  # windows stuff, no worries for linux
        Token2Java(file_path)

def Token2Java(token_file):
    predictions = open(token_file, "r").readlines()
    predictions_asCodeLines = []

    for prediction in predictions:
        tokens, prob = prediction.strip('\n').split('\t')
        tmp = toJavaSourceCode(tokens) + '\t' + prob
        # if tmp != "":
        predictions_asCodeLines.append(tmp)

    if(len(predictions_asCodeLines) == 0):
        sys.stderr.write("All predictions contains <unk> token")
        sys.exit(1)

    # predictions_asCodeLines_file = open(os.path.join(argv[1], "predictions_JavaSource.txt"), "w")
    j_patch_file = 'JavaSource_patches/' + token_file.split('/')[-1].replace(".txt","_JavaSource.txt")
    predictions_asCodeLines_file = open(j_patch_file, "w")
    for predictions_asCodeLine in predictions_asCodeLines:
        predictions_asCodeLines_file.write(predictions_asCodeLine + "\n")
    predictions_asCodeLines_file.close()



def toJavaSourceCode(prediction):
    tokens = prediction.strip().split(" ")
    tokens = [token.replace("<seq2seq4repair_space>", " ") for token in tokens]
    codeLine = ""
    delimiter = JavaDelimiter()
    for i in range(len(tokens)):
        if(tokens[i] == "<unk>"):
            return ""
        if(i+1 < len(tokens)):
            # DEL = delimiters
            # ... = method_referece
            # STR = token with alphabet in it


            if(not isDelimiter(tokens[i])):
                if(not isDelimiter(tokens[i+1])): # STR (i) + STR (i+1)
                    codeLine = codeLine+tokens[i]+" "
                else: # STR(i) + DEL(i+1)
                    codeLine = codeLine+tokens[i]
            else:
                if(tokens[i] == delimiter.varargs): # ... (i) + ANY (i+1)
                    codeLine = codeLine+tokens[i]+" "
                elif(tokens[i] == delimiter.biggerThan): # > (i) + ANY(i+1)
                    codeLine = codeLine+tokens[i]+" "
                elif(tokens[i] == delimiter.rightBrackets and i > 0):
                    if(tokens[i-1] == delimiter.leftBrackets): # [ (i-1) + ] (i)
                        codeLine = codeLine+tokens[i]+" "
                    else: # DEL not([) (i-1) + ] (i)
                        codeLine = codeLine+tokens[i]
                else: # DEL not(... or ]) (i) + ANY
                    codeLine = codeLine+tokens[i]
        else:
            codeLine = codeLine+tokens[i]
    return codeLine

def isDelimiter(token):
    return not token.upper().isupper()

class JavaDelimiter:
    @property
    def varargs(self):
        return "..."

    @property
    def rightBrackets(self):
        return "]"

    @property
    def leftBrackets(self):
        return "["

    @property
    def biggerThan(self):
        return ">"


