#include <iostream>
#include <cstdio>
#include <string>
#include <windows.h>
#include <dirent.h>
#include <cmath>
#include <fstream>
using namespace std;

double priceTable[20][12] = {0};
long long volumeTable[20][12] = {0};
int priceTableNumber[20][12] = {0};
int volumeTableNumber[20][12] = {0};

void output(ofstream& fout){
    for (int i = 0; i <= 5; i++){
        fout << 2012+i << '\t';
        for (int j = 0; j <= 11; j++){
            if (volumeTableNumber[j][i] == 0)
                break;
            fout << volumeTable[j][i]/volumeTableNumber[j][i] << '\t';
        }
        fout << endl;
    }
}

void insertData(int year, int month, int day, double price, long long volume){
    int row = (year-2012);
    int column = (month-1);
    priceTable[column][row] += price;
    volumeTable[column][row] += volume;
    priceTableNumber[column][row]++;
    volumeTableNumber[column][row]++;
}

void parseCSV(ifstream& fin){
    int year, month, day;
    double price;
    long long volume;
    char temp;

    while(fin >> year){
        fin >> temp >> month >> temp >> day >> temp >> price >> temp >> volume;
        insertData(year, month, day, price, volume);
    }
}

int main(){
    string inputFile = "for_c.csv";
    ifstream fin(inputFile.c_str());
    string outputFile = "volume.txt";
    ofstream fout(outputFile.c_str());

    parseCSV(fin);
    output(fout);

    fin.close();
    fout.close();

    return 0;
}
