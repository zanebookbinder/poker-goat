# poker-goat


# Rahul
-function that takes in 1000 training examples of (s,a,s',r)
	-get Q values for s
	-get Q values s', update weight for action that was taken from s in training example (with r + Qmax from s'), leave other Q values untouched
	-fit the model (only one epoch) with (X,y) = (s, updated Q values)

# Zane
-produce training examples using the model's getAction function and store in a list
-when 1000 examples are in the list, call the function above
-repeat