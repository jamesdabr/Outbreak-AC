// T093 intentional instrumentation control, never linked into production.
int main() {
    volatile unsigned char *p=new unsigned char[8];
    volatile unsigned index=8;
    p[index]=1; // Deliberate one-byte heap overrun; ASan must terminate.
    delete[] p;
    return 0;
}
