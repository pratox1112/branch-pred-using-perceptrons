#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <vector>
#include <cmath>
 
typedef unsigned long ulong;
 
using namespace std;
 
// Define constants
#define TAKEN 1
#define NOTTAKEN 0
 
class gshare {
 
protected:
    ulong index, predictions, mispredictions;
    int mask1, mask2, gbhr, predicted_branch, size, iG, h;
    vector<int> predictor_table;
 
public:
    void init(int iG, int h) {
        this->iG = iG;
        this->h = h;
        index = predictions = mispredictions = 0;
        gbhr = 0;
        size = (int) pow(2, (double) iG);
        mask1 = size - 1;
        mask2 = (int) pow(2, (double)(iG - h)) - 1;
        predictor_table.resize(size, TAKEN); // Initialize to TAKEN (1)
    }
 
    void set_index(ulong address){
        ulong temp, xored;
        temp = address >> 2;
        temp = temp & mask1;
        if (h > 0) {
            xored = gbhr ^ (temp >> (iG - h));
            xored = xored << (iG - h);
            temp = temp & mask2;
            index = xored | temp;
        }
        else
            index = temp;
    }
 
    int access(ulong address, int actual_branch){
        predictions++;
        set_index(address);
        predicted_branch = predictor_table[index] == TAKEN ? TAKEN : NOTTAKEN;
        return update_predictor(actual_branch, predicted_branch);
    }
 
    int update_predictor(int actual_branch, int predicted_branch){
        if (actual_branch == TAKEN) {
            if (predictor_table[index] != TAKEN) {
                predictor_table[index] = TAKEN;
            }
            update_gbhr(1);
            if (predicted_branch == NOTTAKEN) {
                mispredictions++;
                return 0;
            }
        }
        else { // NOTTAKEN
            if (predictor_table[index] != NOTTAKEN) {
                predictor_table[index] = NOTTAKEN;
            }
            update_gbhr(0);
            if (predicted_branch == TAKEN) {
                mispredictions++;
                return 0;
            }
        }
        return 1;
    }
 
    void update_gbhr(int i){
        if (h > 0) {
            gbhr = gbhr >> 1;
            gbhr = gbhr | (i << (h - 1));
        }
    }
 
    bool is_taken(ulong address){
        set_index(address);
        return predictor_table[index] == TAKEN ? true : false;
    }
 
    void print_output(){
        cout << "OUTPUT\nnumber of predictions: " << predictions
             << "\nnumber of mispredictions: " << mispredictions
             << fixed << setprecision(2)
             << "\nMisprediction rate: "
             << (float)mispredictions*100/predictions
             << "%\n";
    }
 
    void print_stats(){
        cout << "FINAL GSHARE CONTENTS\n";
        for(int i = 0; i < size; ++i)
            cout << i << "\t" << (predictor_table[i] ? "TAKEN" : "NOT TAKEN") << "\n";
    }
 
};
 
int main(int argc, char* argv[]) {
    // Check for correct usage
    if(argc != 4) {
        cout << "Usage: )" << argv[0] << R"( C:\Users\prato\OneDrive\Desktop\EECE7205 - Fundamentals of CompE\Project\Trace files\insertionsort.txt 10 5)" << "\n";
        cout << "Example: " << argv[0] << " dataset.txt 10 8\n";
        return 1;
    }
 
    string dataset_file = "dataset.txt";
    int iG = atoi(argv[2]); // Number of index bits
    int h = atoi(argv[3]);  // History length
 
    // Initialize the Gshare predictor
    gshare predictor;
    predictor.init(iG, h);
 
    // Open the dataset file
    ifstream infile(dataset_file);
    if(!infile.is_open()) {
        cerr << "Error: Unable to open file " << dataset_file << "\n";
        return 1;
    }
 
    string line;
    // Process each line in the dataset
    while(getline(infile, line)) {
        // Skip empty lines
        if(line.empty()) continue;
 
        // Use a stringstream to parse the line
        stringstream ss(line);
        string address_str;
        int outcome;
 
        ss >> address_str >> outcome;
 
        // Convert hexadecimal address to ulong
        ulong address;
        // Remove any potential '0x' prefix
        if(address_str.find("0x") == 0 || address_str.find("0X") == 0) {
            address = stoul(address_str.substr(2), nullptr, 16);
        }
        else {
            address = stoul(address_str, nullptr, 16);
        }
 
        // Validate outcome
        if(outcome != TAKEN && outcome != NOTTAKEN) {
            cerr << "Warning: Invalid outcome '" << outcome << "' for address " << address_str << ". Skipping.\n";
            continue;
        }
 
        // Access the predictor with the current branch
        predictor.access(address, outcome);
    }
 
    infile.close();
 
    // Print the prediction results
    predictor.print_output();
 
    // Optionally, print the final PHT contents
    // predictor.print_stats();
 
    return 0;
}
