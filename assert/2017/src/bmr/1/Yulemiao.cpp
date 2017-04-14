#include <iostream>
#include <cstdio>
#include <cstring>
using namespace std;

typedef long long ll;

inline ll read(){
    ll a = 0;
    char ch = getchar();
    while(!isdigit(ch)){
        ch = getchar();
    }
    while(isdigit(ch)){
        a = a * 10 + ch - '0';
        ch = getchar();
    }
    return a;
}
int N,M,Q;
struct Mat{
    ll matrix[150][150];
    Mat(){
        memset(matrix,0,sizeof(matrix));
    }
    Mat operator *(const Mat b){
        Mat res;
        for(int i=0;i<=N;++i){
            for(int k=0;k<=N;++k){
                if(matrix[i][k]){
                    for(int j=0;j<=N;++j){
                        res.matrix[i][j] += matrix[i][k] * b.matrix[k][j];
                    }
                }
            }
        }
        return res;
    }
    void clear(){
        memset(matrix,0,sizeof(matrix));
    }
    void init(){
        clear();
        for(int i=0;i<=N;++i){
            matrix[i][i] = 1;
        }
    }
};
Mat mul;
int op;

inline void fastPow(Mat &a,int p){
    Mat base = a;
    a.init();
    while(p){
        if(p & 1){
            a = a * base;
        }
        base = base * base;
        p >>= 1;
    }
}

int main(){
    while(scanf("%d%d%d",&N,&M,&Q) == 3){
        if(N == 0 && M == 0 && Q == 0) break;
        mul.init();
        while(Q--){
            op = read();
            switch(op){
                case 1:{
                    int x;
                    x = read();
                    mul.matrix[0][x] += 1;
                    break;
                }
                case 2:{
                    int x = read();
                    for(int i = 0;i<=N;++i){
                        mul.matrix[i][x] = 0;
                    }
                    break;
                }
                case 3:{
                    int x = read();
                    int y = read();
                    for(int i=0;i<=N;++i){
                        swap(mul.matrix[i][x],mul.matrix[i][y]);
                    }
                    break;
                }
            }
        }
        if(!M){
            for(int i=1;i<N;++i){
                printf("0 ");
            }
            puts("0");
        }else{
            fastPow(mul,M);
            for(int i=1;i<=N;++i){
                printf("%lld ",mul.matrix[0][i]);
            }
            puts("");
        }
    }
    return 0;
}