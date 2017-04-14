#include <iostream>
#include <cstdio>
#include <cstring>
#include <queue>
#include <cstdlib>
using namespace std;

#define INF 1e9

struct Edge{
	int v,w;
	int next;
	Edge(){}
	Edge(int t,int k,int n){
		v = t;
		next = n;
		w = k;
	}
};

Edge e[201000];
int EID = 1;

int First[201000];
int dep[201000];
queue<int> q;
int N,M;

inline void AddEdge(int u,int v,int w){
	e[EID].next = First[u];
	e[EID].v = v;
	e[EID].w = w;
	First[u] = EID++;
}

inline bool bfs(){
	memset(dep, -1, sizeof(dep));
	q.push(1);
	dep[1] = 0;
	int k;
	while(q.size()){
		k = q.front();q.pop();
		for(int i=First[k];i;i=e[i].next){
			int v = e[i].v;
			if(dep[v] == -1 && e[i].w>0){
				dep[v] = dep[k] + 1;
				q.push(v);
			}
		}
	}
	return dep[N] != -1;
}

int dinic(int v,int inf){
	if(v == N) return inf;
	else{
		int f;
		for(int i=First[v];i;i=e[i].next){
			if(dep[e[i].v] == dep[v] + 1 && e[i].w>0){
				f = dinic(e[i].v, min(inf, e[i].w));
				if(f){
					e[i].w -= f;
					e[i^1].w += f;
					return f;
				}
			}
		}
	}
	return 0;
}

inline int read(){
	int a = 0;
	char ch = getchar();
	while(!isdigit(ch)) ch = getchar();
	while(isdigit(ch)){ 
		a = a*10+ch-'0';
		ch=getchar();
	}
	return a;
}

int main(){
	N = read();M=read();int a,b;
	for(int i=1;i<=M;++i){
		a = read();b=read();
		AddEdge(a,b,1);
		AddEdge(b,a,1);
	}
	int ans = 0;int flow;
	while(bfs()){
		while(flow=dinic(1,INF)){
			ans += flow;
		}
	}
	cout<<ans;
	return 0;
}