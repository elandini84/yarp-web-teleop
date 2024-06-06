################################################################################
#                                                                              #
# Copyright (C) 2020 Fondazione Istituto Italiano di Tecnologia (IIT)          #
# All Rights Reserved.                                                         #
#                                                                              #
################################################################################

set(appname webserver)

file(GLOB apps      ${CMAKE_CURRENT_SOURCE_DIR}/scripts/*.xml)
file(GLOB conf      ${CMAKE_CURRENT_SOURCE_DIR}/conf/*.ini)
file(GLOB robotInterface      ${CMAKE_CURRENT_SOURCE_DIR}/conf/robotInterface/*.xml)

yarp_install(FILES ${apps}    DESTINATION ${YARP-WEB-TELEOP_APPLICATIONS_INSTALL_DIR})
yarp_install(FILES ${conf}    DESTINATION ${YARP-WEB-TELEOP_CONTEXTS_INSTALL_DIR}/${appname})
yarp_install(FILES ${robotInterface}    DESTINATION ${YARP-WEB-TELEOP_CONTEXTS_INSTALL_DIR}/${appname}/robotInterface)
