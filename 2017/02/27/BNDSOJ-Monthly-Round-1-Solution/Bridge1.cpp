#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <cstring>
#include <string>
#include <algorithm>

using namespace std;

struct ex {
	int t;
	int w;
	int next;
};

int inf = 1000000007;

ex e[200005];
int eb[10005];
int ec = -1;

int dist[10005];

int q[10005];
int pf, pe;

int n, m;

int read(){
	int x = 0;
	char ch = getchar();
	
	while('0' > ch or ch > '9'){
		ch = getchar();
	}
	
	while('0' <= ch and ch <= '9'){
		x = x * 10 + ch - '0';
		ch = getchar();
	}
	
	return x;
}

int addedge(int x, int y, int w){
	ec++;
	e[ec].t = y;
	e[ec].w = w;
	e[ec].next = eb[x];
	eb[x] = ec; 
	
	return 0;
}

bool bfs(){
	int enow;
	int x, y;
	
	memset(dist, -1, sizeof(dist));
	
	pf = 1;
	pe = 1;
	q[pe] = 1;
	dist[1] = 0;
	
	while(pf <= pe){
		x = q[pf];
		
		enow = eb[x];
		
		while(enow != -1){
			y = e[enow].t;
			if(dist[y] == -1 and e[enow].w > 0){
				dist[y] = dist[x] + 1;
				pe++;
				q[pe] = y;
			}
			enow = e[enow].next;
		}
		
		pf++;
	}
	
	return dist[n] != -1;
}

int find(int x, int maxf){
	int y;
	int enow;
	int flow;
	
	if(x == n){
		return maxf;
	}
	
	enow = eb[x];
	
	while(enow != -1){
		y = e[enow].t;
		if(e[enow].w > 0 and dist[y] == dist[x] + 1){
			flow = find(y, min(maxf, e[enow].w));
			
			if(flow){
				e[enow].w -= flow;
				e[enow ^ 1].w += flow;
				return flow;
			}
			
		}
		
		enow = e[enow].next; 
	}
	
	return 0;
}

int main(){
	
	int i, j;
	int ans = 0, flow;
	int x, y;
	
	n = read();
	m = read();
	
	memset(eb, -1, sizeof(eb));
	
	for(i=1;i<=m;i++){
		x = read();
		y = read();
		addedge(x, y, 1);
		addedge(y, x, 1);
	}
	
	while(bfs()){
		while(flow = find(1, inf)){
			ans += flow;
		}
	}
	
	printf("%d\n", ans);
	
	return 0;
}