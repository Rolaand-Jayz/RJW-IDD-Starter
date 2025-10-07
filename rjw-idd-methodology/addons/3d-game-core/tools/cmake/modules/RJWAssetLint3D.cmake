# RJWAssetLint3D.cmake — helper for invoking the 3D asset linter
include_guard(GLOBAL)

function(rjw3d_register_asset_lint ASSET_ROOT PROFILE)
  if(NOT EXISTS "${CMAKE_SOURCE_DIR}/addons/3d-game-core/tools/asset_linter_3d.py")
    message(FATAL_ERROR "asset_linter_3d.py not found. Ensure add-in is checked out.")
  endif()
  add_custom_target(rjw3d_asset_lint
    COMMAND ${CMAKE_COMMAND} -E env
            RJW3D_PROFILE=${PROFILE}
            python ${CMAKE_SOURCE_DIR}/addons/3d-game-core/tools/asset_linter_3d.py
              --assets ${ASSET_ROOT}
              --profile ${PROFILE}
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMENT "RJW-IDD 3D: asset lint for profile ${PROFILE}")
endfunction()
