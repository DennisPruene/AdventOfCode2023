#![allow(non_snake_case)]
mod circuit;
mod module;

use circuit::Circuit;
use regex::Regex;
use std::collections::HashMap;
use std::fs;
use std::path::Path;

fn main() {
    let mut circuit = parse_file("input");
    println!("{circuit:#?}");
    let mut low_pulse_count = 0;
    let mut high_pulse_count = 0;
    for _ in 0..1000 {
        let (dl, dh) = circuit.press_button_and_count_pulses();
        low_pulse_count += dl;
        high_pulse_count += dh;
    }
    println!("{low_pulse_count}, {high_pulse_count}");
    circuit.reset();

    let watch_for = vec!["gv", "ll", "rc", "qf"];
    let watch_for_indices: Vec<usize> = watch_for
        .iter()
        .map(|name| circuit.get_index(name))
        .collect();
    let logs = circuit.press_button_n_times(10000);
    let mut filtered_logs: HashMap<String, Vec<(usize, usize)>> = watch_for
        .iter()
        .map(|name| (name.to_string(), vec![]))
        .collect();
    for (press_index, log) in logs.iter().enumerate() {
        for (&watch_for_name, &watch_for_index) in watch_for.iter().zip(watch_for_indices.iter()) {
            for (turn_index, _) in log[watch_for_index].iter().filter(|(_, pu)| !*pu) {
                filtered_logs
                    .get_mut(watch_for_name)
                    .unwrap()
                    .push((press_index + 1, *turn_index))
            }
        }
    }
    println!("{:#?}", filtered_logs);

    /*let mut low_pulse_count = 0;
    let mut high_pulse_count = 0;
    for _ in 0..1000 {
        let (dl, dh, _) = press_button(&mut modules, "output");
        low_pulse_count += dl;
        high_pulse_count += dh;
        button_presses += 1;
    }
    println!("{low_pulse_count} {high_pulse_count} {button_presses}");*/
}

/*lazy_static! {
    static ref RE = Regex::new("(broadcaster|%|&)([a-z]*) -> ([a-z, ]+)").unwrap();
}*/

fn parse_file(filename: impl AsRef<Path>) -> Circuit {
    let mut module_prefixes = vec![];
    let mut module_names_raw = vec![];
    let mut destination_modules_raw = vec![];
    for (module_prefix, module_name, destinations) in fs::read_to_string(filename)
        .unwrap()
        .lines()
        .map(parse_line)
    {
        module_prefixes.push(module_prefix);
        module_names_raw.push(module_name);
        destination_modules_raw.push(destinations);
    }
    Circuit::new(module_prefixes, module_names_raw, destination_modules_raw)
}

fn parse_line(line: &str) -> (String, String, Vec<String>) {
    let RE = Regex::new("(broadcaster|%|&)([a-z]*) -> ([a-z, ]+)").unwrap();
    let captures = RE.captures(line).unwrap();
    let module_prefix = captures.get(1).unwrap().as_str();
    let module_name = captures.get(2).unwrap().as_str();
    let destination_modules = captures.get(3).unwrap().as_str();
    let destination_modules: Vec<String> = destination_modules
        .split(", ")
        .map(|s| s.to_string())
        .collect();
    if module_prefix == "broadcaster" {
        (
            "".to_string(),
            "broadcaster".to_string(),
            destination_modules,
        )
    } else {
        (
            module_prefix.to_string(),
            module_name.to_string(),
            destination_modules,
        )
    }
}
