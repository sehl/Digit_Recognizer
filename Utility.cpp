#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;

/* No line in the training data file can be longer than the product of the
 * image dimensions times the max char length of a var value + 1 */
const size_t MAX_LINE_LENGTH = 28 * 28 * 4;
const size_t MAX_WORDS_PER_LINE = 28 * 28 + 1;
/* train.csv contains 42001 lines (including label line) */
const size_t NUM_LINES = 42000;

/* Iterates through the given string, seeking the delimiting character,
 * splitting the string into a vector */
vector<string>* split_str(string s, char delim)
{
	vector<string>* v = new vector<string>(MAX_WORDS_PER_LINE);
	size_t start; 
	size_t end;
	start = 0;
	;

	while ( ( end = s.find( delim, start ) ) > string::npos )
	{
		 size_t len = end - start;
		 v->push_back( s.substr( start, len ) );
		 start = end + 1;
	}

	// Fencepost - get the last value
	end = s.length();
	v->push_back( s.substr( start, end - start ) );

	return v;
}

/* Reads the provided test data file, shuffles it, then saves to two separate
 * files: train_x.csv and train_y.csv */
int main()
{
	/* (C-style) Array into which to store the data vectors */
	vector< vector<string>* > data;

	// Read in data file
	ifstream f;
	f.open("./data/train.csv");

	// throw the first line away
	string text;
	getline( f, text );

	// Iterate through the lines of the file and store values
	while ( getline (f, text, ',') )
	{
		vector<string>* v = new vector<string>();
		v->push_back(text);
		getline(f, text);
		v->push_back(text);

		data.push_back( v );
	}

	// Shuffle the data and save as new data files
	random_shuffle( data.begin(), data.end() );

	ofstream train_x, train_y;
	train_x.open("./data/train_x.csv");
	train_y.open("./data/train_y.csv");
	
	size_t i;
	for ( i = 0; i < data.size(); i++ )
	{
		vector<string> item = *data[i];
		train_y << item[0] << '\n';
		train_x << item[1] << '\n';
	}

	train_x.flush();
	train_y.flush();

	f.close();
	train_x.close();
	train_y.close();
}
