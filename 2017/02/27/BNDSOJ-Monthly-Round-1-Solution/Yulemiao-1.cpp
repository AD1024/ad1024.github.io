#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <cstring>
#include <string>
#include <algorithm>

using namespace std;

long long n, m, q;

struct ex{
    long long op;
    long long x;
    long long y;
};

ex op[105];

int se[105];
int fa[105];

long long ar[105];
long long br[105];
long long ans[105];
long long tmpans[105];

bool v[105];
int que[105];
int cnt = 0;

long long l;
long long r;

long long read(){
    int x;
    scanf("%lld", &x);
    return x;
}

int find(int x){
    if(fa[x] != x){
        fa[x] = find(fa[x]);
    }
    
    return fa[x];
}

int join(int x, int y){
    int ra = find(x);
    int rb = find(y);
    
    if(ra != rb){
        fa[rb] = ra;
    }
    
    return 0;
}

int init(){
    int i, j;
    int tmp;
    
    for(i=1;i<=n;i++){
        se[i] = i;
        fa[i] = i;
    }
    
    memset(v, 0, sizeof(v));
    
    for(i=1;i<=q;i++){
        if(op[i].op == 3){
            tmp = se[op[i].x];
            se[op[i].x] = se[op[i].y];
            se[op[i].y] = tmp;
        }
    }
    
    for(i=1;i<=n;i++){
        join(i, se[i]);
    }
    
    return 0;
}

int readop(){
    int i, j;
    
    for(i=1;i<=q;i++){
        op[i].op = read();
        op[i].x = read();
        if(op[i].op == 3){
            op[i].y = read();
        }
    }
    
    return 0;
}

int sem(){
    int i, j, k;
    long long tmp;
    
    memset(ar, 0, sizeof(ar));
    memset(br, 0, sizeof(br));
    memset(ans, 0, sizeof(ans));
    memset(v, 0, sizeof(v));
    
    if(2 * n >= m){
        for(i=1;i<=m;i++){
            for(j=1;j<=q;j++){
                if(op[j].op == 1){
                    ans[op[j].x]++;
                }else if(op[j].op == 2){
                    ans[op[j].x] = 0;
                }else{
                    tmp = ans[op[j].x];
                    ans[op[j].x] = ans[op[j].y];
                    ans[op[j].y] = tmp;
                }
                
            }
            
        }
    }else{
        for(i=1;i<=n;i++){
            if(v[i]){
                continue;
            }
            cnt = 0;
            for(j=i;j<=n;j++){
                if(find(i) == find(j)){
                    v[j] = true;
                    cnt++;
                    que[cnt] = j;
                }
            }
            
            l = 0;
            
            for(j=1;j<=cnt;j++){
                if(se[que[j]] != que[j]){
                    l++;
                }
            }
            
            if(l == 0){
                l = 1;
            }
            
            l *= 2;
            
            memset(ar, 0, sizeof(ar));
            memset(br, 0, sizeof(br));
            memset(tmpans, 0, sizeof(tmpans));
            
            for(k=1;k<=l;k++){
                for(j=1;j<=q;j++){
                    if(op[j].op == 1){
                        ar[op[j].x]++;
                    }else if(op[j].op == 2){
                        ar[op[j].x] = 0;
                    }else{
                        tmp = ar[op[j].x];
                        ar[op[j].x] = ar[op[j].y];
                        ar[op[j].y] = tmp;
                    }
                
                }
            
            }
            
            for(j=1;j<=n;j++){
                br[j] = ar[j];
            }
            
            for(k=1;k<=l;k++){
                for(j=1;j<=q;j++){
                    if(op[j].op == 1){
                        br[op[j].x]++;
                    }else if(op[j].op == 2){
                        br[op[j].x] = 0;
                    }else{
                        tmp = br[op[j].x];
                        br[op[j].x] = br[op[j].y];
                        br[op[j].y] = tmp;
                    }
                
                }
            
            }
            
            r = (m - 2 * l) / l;
            
            for(j=1;j<=n;j++){
                tmpans[j] = br[j] + (br[j] - ar[j]) * r;
            }
            
            r = m % l;
            
            for(k=1;k<=r;k++){
                for(j=1;j<=q;j++){
                    if(op[j].op == 1){
                        tmpans[op[j].x]++;
                    }else if(op[j].op == 2){
                        tmpans[op[j].x] = 0;
                    }else{
                        tmp = tmpans[op[j].x];
                        tmpans[op[j].x] = tmpans[op[j].y];
                        tmpans[op[j].y] = tmp;
                    }
                
                }
            
            }
            
            for(j=1;j<=cnt;j++){
                ans[que[j]] = tmpans[que[j]];
            }
            
        }
    }
    
    return 0;
}

int printans(){
    int i, j;
    
    for(i=1;i<=n;i++){
        printf("%lld ", ans[i]);
    }
    
    printf("\n");
    
    return 0;
}

int main() {
    
    int i, j;
    
    n = read();
    m = read();
    q = read();
    
    while(!(n == 0 and m == 0 and q == 0)){
        
        readop();
        init();
        sem();
        printans();
        
        n = read();
        m = read();
        q = read();
    }
    
    return 0;
}