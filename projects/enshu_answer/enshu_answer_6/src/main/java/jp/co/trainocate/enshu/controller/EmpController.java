package jp.co.trainocate.enshu.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;

import jp.co.trainocate.enshu.entity.Employee;
import jp.co.trainocate.enshu.entity.Location;
import jp.co.trainocate.enshu.form.EmpForm;
import jp.co.trainocate.enshu.repository.EmpRepository;
import jp.co.trainocate.enshu.repository.LocationRepository;

@Controller
public class EmpController {
	@Autowired
	private EmpRepository empRepo;

	@Autowired
	private LocationRepository locRepo;

	@GetMapping("/")
	public String index() {
		return "index";
	}

	//演習6.2-a 正解
	@GetMapping("/findAll")
	public String findAll(Model model) {
		List<Employee> list = empRepo.findAll();
		model.addAttribute("empList", list);
		return "emp_list";
	}

	//演習6.3-a 正解
	@GetMapping("/showFindById")
	public String showFindById(int id, Model model) {
		Employee emp = empRepo.findById(id).orElse(null);
		model.addAttribute("emp", emp);
		return "emp";
	}

	//演習6.4-a 正解
	@GetMapping("/showFindByIdSafe")
	public String showFindByIdSafe(int id, Model model) {
		Employee emp = empRepo.findById(id).orElse(null);
		model.addAttribute("emp", emp);
		return "emp2";
	}

	//演習6.5-a 正解

	@GetMapping("/showInputView")
	public String showInputView(Model model) {
		List<Location> list = locRepo.findAll();
		model.addAttribute("locations", list);
		return "emp_input";

	}

	@PostMapping("/insertEmp")
	public String insertEmp(EmpForm empForm, Model model) {
		Employee emp = new Employee();
		emp.setName(empForm.getName());
		emp.setPassword(empForm.getPassword());
		emp.setSalary(empForm.getSalary());
		//演習6.5-d 正解
		emp.setLocationId(empForm.getLocationId());
		
		emp = empRepo.save(emp);
		model.addAttribute("emp", emp);
		return "result";
	}

	//演習6.6-a 正解
	@GetMapping("/showSearchForm")
	public String showSearchForm(Model model) {
	    List<Location> list = locRepo.findAll();
	    model.addAttribute("locationList", list);
	    return "emp_search";
	}
	
	//演習6.6-d 正解
	@GetMapping("/findHighSalary")
	public String findHighSalary(int salary, String locationName, Model model) {
	    List<Employee> list = empRepo.findHighSalaryByLocation(salary, locationName);
	    model.addAttribute("empList", list);
	    return "emp_list";
	}
	
	@GetMapping("/delete/{id}")
	public String deleteEmp(@PathVariable int id) {
		empRepo.deleteById(id);
		return "redirect:/findAll";
	}
}