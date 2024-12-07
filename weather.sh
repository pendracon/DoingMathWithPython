#!/usr/bin/bash
REQUIREMENTS=${REQUIREMENTS:-".requirements.txt"}
HOME_DIR=${HOME_DIR:-"$(dirname $0)"}
EXEC=${EXEC:-"${HOME_DIR}/weather/app"}
MAIN=${MAIN:-"${HOME_DIR}/weather/app.py"}

export PATH=${HOME}/bin:${PATH}

error () {
    EXE=$1
    echo "${EXE} not found. ${EXE} is required to run this program."
    exit 5
}

export PYTHONPATH=${HOME_DIR}/lib:${HOME_DIR}:${PYTHONPATH} 

# Try the pyinstaller executable first...
if [ -x $EXEC ]; then
    $EXEC --help 2>&1 > /dev/null
    if [ $? -eq 0 ]; then
        $EXEC $*
        exit 0
    fi
fi

# Try the python 3 executable next:
PYTHON=$(which python3)
if [ $? != 0 ]; then
    error "python3"
fi

# Verify dependencies are installed...
if [ ! -d ${HOME_DIR}/lib/sqlalchemy ]; then
    PIP=$(which pip3)
    if [ $? != 0 ]; then
        error "pip3"
    fi

    $PIP list | grep -i sqlalchemy 2>&1 > /dev/null
    if [ $? != 0 ]; then
        mkdir -p ${HOME_DIR}/lib 2>&1 > /dev/null
        $PIP install -r $REQUIREMENTS -t ${HOME_DIR}/lib
    fi
fi

# Rotate current log file
if [ -f ${HOME_DIR}/logs/weather-plotter.log ]; then
    LDATE=$(tail -1 logs/weather-plotter.log | cut -f1 -d' ' | tr -d '-')
    IDX=$(expr $(ls -1 logs/weather-plotter.log.${LDATE}* 2>/dev/null | wc -l) + 1)
    mv ${HOME_DIR}/logs/weather-plotter.log ${HOME_DIR}/logs/weather-plotter.log.${LDATE}.${IDX}
fi

# ...and run the script!
pushd $HOME_DIR > /dev/null 2>&1
$PYTHON $MAIN $*
popd > /dev/null 2>&1
