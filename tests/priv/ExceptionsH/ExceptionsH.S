
///////////////////////////////////////////
// ExceptionsH.S
//
//
// Purpose: Functional coverage test for Exceptions in M mode
//
// SPDX-License-Identifier: Apache-2.0
///////////////////////////////////////////

##### START_TEST_CONFIG #####
# REQUIRED_EXTENSIONS: [H, I, Zicsr]
# MARCH: rv${XLEN}i_zicsr
# CONFIG_DEPENDENT: true
##### END_TEST_CONFIG #####

#include "WALLY-init-lib.h"

main:


finished:
    j done
