package jp.co.trainocate.enshu.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import jp.co.trainocate.enshu.entity.Employee;

public interface EmpRepository extends JpaRepository<Employee, Integer>{
	
}
