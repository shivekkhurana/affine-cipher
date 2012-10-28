#include <iostream>
using namespace std;

//defines
#define MATRIX_SIZE 5
#define MS 3

//prototypes
int print_2d(int m[MS][MS]);

int main(){
  int a[MS][MS] = {{0,1,2},{3,4,5},{6,7,8}};
  //print_2d(a);
  cout << a[0][0];
  print_2d(a);
  return 0;
}

int print_2d(int m[MS][MS]){
  int temp;
  for(int i=0; i<MS; ++i){
    for(int j=0; j<MS; ++j){
      temp = m[i][j];
      cout << temp << "\t";
    }
    cout << '\n';
  }
  return 0;
}

