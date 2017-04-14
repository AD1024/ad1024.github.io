#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <cstring>
#include <string>
#include <algorithm>

using namespace std;

const int maxn = 1e7 + 5;
long long mod = 1e9 + 7;

int m, n;

long long qpow(long long b, long long x){
	long long ans = 1;
	while(x > 0){
		if(x % 2){
			ans = ans * b % mod;
		}
		
		b = b * b % mod;
		x = x / 2;
	}
	return ans;
}

long long getc(int x, int y){
	long long sa = 1, sb = 1;
	
	for(int i=0;i<y;i++){
		sa = sa * (x - i) % mod;
		sb = sb * (i + 1) % mod;
	}
	return sa * qpow(sb, mod - 2) % mod;
}

int main(){
	int i, j;
	
	cin >> n >> m;
	
	cout << getc(n + m - 1, min(n, m - 1)) << endl;
	
	return 0;
}