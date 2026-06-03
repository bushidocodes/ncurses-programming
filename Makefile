CC      = gcc
CFLAGS  = -Wall -Wextra -Wno-unused-result -Wno-implicit-fallthrough \
          -Werror -fsanitize=address,undefined -fno-omit-frame-pointer
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
