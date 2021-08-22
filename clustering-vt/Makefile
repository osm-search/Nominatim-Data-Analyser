CFLAGS += -I include --std=c++17

export MASON_DIR = $(shell pwd)/.mason
export MASON = $(MASON_DIR)/mason

SUPERCLUSTER = supercluster 0.3.2
KDBUSH = kdbush 0.1.3
RAPIDJSON = rapidjson 1.1.0
GEOMETRY = geometry 1.0.0
GEOJSON = geojson 0.4.3
VARIANT = variant 1.2.0
VTZERO = vtzero 1.1.0
PROTOZERO = protozero 1.7.0

DEPS = `$(MASON) cflags $(SUPERCLUSTER)` `$(MASON) cflags $(KDBUSH)` `$(MASON) cflags $(GEOJSON)` `$(MASON) cflags $(GEOMETRY)` `$(MASON) cflags $(VARIANT)` `$(MASON) cflags $(VTZERO)` `$(MASON) cflags $(PROTOZERO)`
RAPIDJSON_DEP = `$(MASON) cflags $(RAPIDJSON)`

default:
	make build/clustering-vt

$(MASON):
ifeq (,$(wildcard $(MASON)))
		rm -f -R ${MASON_DIR}
		git submodule update --init --recursive --force
endif

mason_packages: $(MASON)
	$(MASON) install $(SUPERCLUSTER)
	$(MASON) install $(KDBUSH)
	$(MASON) install $(RAPIDJSON)
	$(MASON) install $(GEOJSON)
	$(MASON) install $(GEOMETRY)
	$(MASON) install $(VARIANT)
	$(MASON) install $(VTZERO)
	$(MASON) install $(PROTOZERO)

build/clustering-vt: clustering-vt.cpp mason_packages Makefile
	mkdir -p build
	$(CXX) clustering-vt.cpp $(CFLAGS) -O3 $(DEPS) $(RAPIDJSON_DEP) -o build/clustering-vt

clean:
	rm -rf build
