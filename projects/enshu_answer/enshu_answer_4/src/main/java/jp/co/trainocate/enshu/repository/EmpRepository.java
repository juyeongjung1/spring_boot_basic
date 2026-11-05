package jp.co.trainocate.enshu.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import jp.co.trainocate.enshu.entity.Employee;

public interface EmpRepository extends JpaRepository<Employee, Integer>{
	List<Employee> findBySalary(Integer salary);
	List<Employee> findByNameLike(String name);
	
	//演習4.1
	Employee findByIdAndPassword(Integer id, String password);
}
