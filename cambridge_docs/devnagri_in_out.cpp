#include <cstdio>
using namespace std;

int main()
{
  char  *devnagri;
  char temp;
  int i;
  for(i=0; (temp = getchar()) != '\n'; i++){
    *(devnagri + i) = temp;
  }
  *(devnagri+i) = '\0';
  for(i=0; (temp = *(devnagri+i++)) != '\0'; putchar(temp));
  return 0;
}
