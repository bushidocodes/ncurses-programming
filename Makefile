CC      = gcc
CFLAGS  = -Wall -Wextra -Wno-unused-result -Wno-implicit-fallthrough
LIBS    = -lncursesw
BINDIR  = bin

SRCS    := $(wildcard *.c)
BINS    := $(patsubst %.c,$(BINDIR)/%,$(SRCS))

.PHONY: all clean

all: $(BINDIR) $(BINS)

$(BINDIR):
	mkdir -p $(BINDIR)

$(BINDIR)/%: %.c
	$(CC) $(CFLAGS) -o $@ $< $(LIBS)

clean:
	rm -rf $(BINDIR)
