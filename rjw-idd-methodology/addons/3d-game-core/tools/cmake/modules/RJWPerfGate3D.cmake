# RJWPerfGate3D.cmake — helper functions for the 3D game core add-in
include_guard(GLOBAL)

function(rjw3d_register_perf_gate TARGET_METRICS PROFILE)
  if(NOT EXISTS "${CMAKE_SOURCE_DIR}/addons/3d-game-core/tools/perf_budget_gate_3d.py")
    message(FATAL_ERROR "perf_budget_gate_3d.py not found. Ensure add-in is checked out.")
  endif()
  add_custom_target(rjw3d_perf_gate
    COMMAND ${CMAKE_COMMAND} -E env
            RJW3D_PROFILE=${PROFILE}
            python ${CMAKE_SOURCE_DIR}/addons/3d-game-core/tools/perf_budget_gate_3d.py
              --metrics ${TARGET_METRICS}
              --profile ${PROFILE}
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMENT "RJW-IDD 3D: perf budget gate for profile ${PROFILE}")
endfunction()
