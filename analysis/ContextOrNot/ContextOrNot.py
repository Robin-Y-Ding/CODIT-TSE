keywords = set(['abstract', 'assert', 'boolean', 'break', 'byte', 'case',
                  'catch', 'char', 'class', 'const', 'continue', 'default',
                  'do', 'double', 'else', 'enum', 'extends', 'final',
                  'finally', 'float', 'for', 'goto', 'if', 'implements',
                  'import', 'instanceof', 'int', 'interface', 'long', 'native',
                  'new', 'package', 'private', 'protected', 'public', 'return',
                  'short', 'static', 'strictfp', 'super', 'switch',
                  'synchronized', 'this', 'throw', 'throws', 'transient', 'try',
                  'void', 'volatile', 'while'])

separators = set(['(', ')', '{', '}', '[', ']', ';', ',', '.'])

operators = set(['>>>=', '>>=', '<<=',  '%=', '^=', '|=', '&=', '/=',
                  '*=', '-=', '+=', '<<', '--', '++', '||', '&&', '!=',
                  '>=', '<=', '==', '%', '^', '|', '&', '/', '*', '-',
                  '+', ':', '?', '~', '!', '<', '>', '=', '...', '->', '::'])

booleans = set(["true", "false"])


def ContextOrNot():
	pre = open("PreSmallToken.txt", 'r')
	post = open("PostSmallToken.txt", 'r')
	logFile = open("log.txt", 'w')
	preLines = pre.readlines()
	total = len(preLines)
	postLines = post.readlines()
	cnt = 0
	for idx, l in enumerate(preLines):
		buggySet = set(l.strip().split('\t'))
		patchSet = set(postLines[idx].strip().split('\t'))
		newToken = 0
		tokens = list()
		for t in patchSet:
			if t not in keywords and t not in separators and \
				t not in operators and t not in booleans and \
				t not in buggySet and not t.isdigit():
				newToken = 1
				tokens.append(t)
		cnt += newToken
		tokenStr = ' '.join(tokens) + '\n'
		logFile.write(tokenStr)

	print ("Total one line bugs: " + str(total) + '\n')
	print ("Bugs which introduce new token: " + str(cnt) + '\n')
	print ("Ratio: " + str(cnt / total))


ContextOrNot()
