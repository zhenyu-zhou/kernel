#include <stdio.h>
#include <string.h>
#include <malloc.h>

char* cut(char* s, char* tag1, char* tag2, int len)
{
	void* first = strstr(s, tag1);
	if(first == NULL)
		return ;
	void* second = strstr(first+strlen(tag1), tag2);
	if(second == NULL)
	{
		// assume segment impossible
		printf("Only match once!\n");
		return ;
	}
	void* p = second+strlen(tag2);
	// printf("first: %.*s\n", (int)strlen(first), first);
	// printf("second: %.*s\n", (int)strlen(second), second);
	// printf("p: %.*s\n", (int)strlen((char*)p), (char*)p);

	/*while(first != second && p != s+len)
	{
		printf("haha: %c %c\n", *first, *p);
		*((unsigned char*)first) = *p;
		printf("first: %.*s\n", (int)strlen((char*)first), (char*)first);
		first++; p++;
	}
	if(p == s+len)
	{
		*first = '\0';
		return ;
	}*/
	
	void* ret = malloc(100);
        memcpy(ret, first+strlen(tag1), second-first-strlen(tag1));
	*((char*)(ret+(second-first-strlen(tag1)))) = '\0';

	memcpy(first, p, strlen(p));
	*((char*)(first+strlen(p))) = '\0';
	
	return ret;
}

int main()
{
	char* tag1 = "@#$zzy";
	char* tag2 = "zzy@#$";
	char* s = (char*)malloc(100);
	char* cs = "1234@#$zzy567zzy@#$890";
	memcpy(s, cs, strlen(cs));
	int len = strlen(s);
	printf("ori: %.*s\n", len, s);
	char* mid = cut(s, tag1, tag2, len);
	printf("after: %.*s\n", len, s);
	printf("mid: %s\n", mid);
}
