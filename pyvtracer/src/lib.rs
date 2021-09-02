mod config;
mod converter;
mod svg;

use crate::config::path_simplify_mode_from_str;
use std::str::FromStr;
use std::path::PathBuf;
pub use config::*;
pub use converter::*;
pub use svg::*;

use pyo3::prelude::*;

#[pyfunction]
fn convert_to_svg(input_path: &str,
    color_mode: &str,
    hierarchical: &str,
    mode: &str,
    filter_speckle: usize,
    color_precision: i32,
    gradient_step: i32,
    corner_threshold: i32,
    segment_length: f64,
    splice_threshold: i32,
    path_precision: u32
) -> String {
    let mut config = Config::default();
    config.input_path = PathBuf::from(input_path);
    config.color_mode = ColorMode::from_str(color_mode).unwrap();
    config.hierarchical = Hierarchical::from_str(hierarchical).unwrap();
    config.mode = path_simplify_mode_from_str(mode);
    config.filter_speckle = filter_speckle;
    config.color_precision = color_precision;
    config.layer_difference = gradient_step;
    config.corner_threshold = corner_threshold;
    config.length_threshold = segment_length;
    config.splice_threshold = splice_threshold;
    config.path_precision = Some(path_precision);

    let result = convert_image_to_svg(config);
    match result {
        Ok(svg) => svg,
        Err(e) => panic!("convert error! : {}", e)
    }
}


#[pyfunction]
fn convert_to_svg_file(input_path: &str,
    output_path: &str,
    color_mode: &str,
    hierarchical: &str,
    mode: &str,
    filter_speckle: usize,
    color_precision: i32,
    gradient_step: i32,
    corner_threshold: i32,
    segment_length: f64,
    splice_threshold: i32,
    path_precision: u32
) {
    let mut config = Config::default();
    config.input_path = PathBuf::from(input_path);
    config.output_path = PathBuf::from(output_path);
    config.color_mode = ColorMode::from_str(color_mode).unwrap();
    config.hierarchical = Hierarchical::from_str(hierarchical).unwrap();
    config.mode = path_simplify_mode_from_str(mode);
    config.filter_speckle = filter_speckle;
    config.color_precision = color_precision;
    config.layer_difference = gradient_step;
    config.corner_threshold = corner_threshold;
    config.length_threshold = segment_length;
    config.splice_threshold = splice_threshold;
    config.path_precision = Some(path_precision);
    
    if let Err(e) = convert_image_to_svg_file(config) {
        panic!("fail to convert image : {}", e);
    }
}

#[pymodule]
fn vlib(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(convert_to_svg_file, m)?)?;
    m.add_function(wrap_pyfunction!(convert_to_svg, m)?)?;
    Ok(())
}