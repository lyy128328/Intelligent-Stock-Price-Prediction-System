#include <iostream>
#include <cstdio>
using namespace std;

int dataTable[10][1300] = {0};

void zeroParent(int x){
    double T = 0;
    double F = 0;
    x--;

    for (int i = 0; i < 1258; i++){
        if (dataTable[x][i] == 1)
            T++;
        else
            F++;
    }

    cout << x+1 << ": " << endl;
    cout << "T: " << T/(T+F) << endl;
    cout << "F: " << F/(T+F) << endl;
    cout << endl;
}

void twoParent(int a, int b, int x){
    int bin = 0;
    a--;
    b--;
    x--;

    cout << x+1 << ": " << endl;
    for (int k = 0; k < 4; k++){
        double T = 0;
        double F = 0;

        for (int i = 0; i < 1258; i++){
            if ((dataTable[a][i] == bin/2)&&(dataTable[b][i] == bin%2/1)){
                if (dataTable[x][i] == 1)
                    T++;
                else
                    F++;
            }
        }

        cout << bin/2 << bin%2/1 << " T: ";
        cout << T/(T+F) << endl;
        cout << bin/2 << bin%2/1 << " F: ";
        cout << F/(T+F) << endl;
        bin++;
    }
    cout << endl;
}

void fourParent(int a, int b, int c, int d, int x){
    int bin = 0;
    a--;
    b--;
    c--;
    d--;
    x--;

    cout << x+1 << ": " << endl;
    for (int k = 0; k < 16; k++){
        double T = 0;
        double F = 0;

        for (int i = 0; i < 1258; i++){
            if ((dataTable[a][i] == bin/8)&&(dataTable[b][i] == bin%8/4)
                &&(dataTable[c][i] == bin%4/2)&&(dataTable[d][i] == bin%2/1)){
                if (dataTable[x][i] == 1)
                    T++;
                else
                    F++;
            }
        }

        cout << bin/8 << bin%8/4 << bin%4/2 << bin%2/1 << " T: ";
        cout << T/(T+F) << endl;
        cout << bin/8 << bin%8/4 << bin%4/2 << bin%2/1 << " F: ";
        cout << F/(T+F) << endl;
        bin++;
    }
    cout << endl;
}

int main(){
    int data = 0;
    freopen("data.csv", "r", stdin);
    freopen("CPT.txt", "w", stdout);

    for (int i = 0; i < 1258; i++){
        for (int j = 0; j < 10; j++){
            scanf("%d", &data);
            getchar();
            dataTable[j][i] = data;
        }
    }

    zeroParent(1);
    zeroParent(2);
    twoParent(1, 2, 3);
    twoParent(1, 3, 4);
    twoParent(1, 3, 5);
    zeroParent(6);
    zeroParent(7);
    fourParent(4, 5, 6, 7, 8);
    twoParent(4, 5, 9);
    fourParent(4, 5, 8, 9, 10);

    return 0;
}
