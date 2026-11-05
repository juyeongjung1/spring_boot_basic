package jp.co.trainocate.answer.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class BootStrapController {
	
	@GetMapping("/7-2")
	public String showBootStrapSetup() {
		return "bootstrap_setup";
	}
    
    @GetMapping("/7-3")
	public String showStyleSample() {
		return "style_sample";
	}
    
    @GetMapping("/7-4")
	public String showTableSample() {
		return "table_sample";
	}
    
    @GetMapping("/7-5")
   	public String showGridSample() {
   		return "grid_sample";
   	}
    
    @GetMapping("/7-5-2")
   	public String showGridSample2() {
   		return "grid_sample2";
   	}
    
    @GetMapping("/7-6")
   	public String showFormSample() {
   		return "form_sample";
   	}
    
    @GetMapping("/7-6-2")
   	public String showFormSample2() {
   		return "form_sample2";
   	}
	
   
}
