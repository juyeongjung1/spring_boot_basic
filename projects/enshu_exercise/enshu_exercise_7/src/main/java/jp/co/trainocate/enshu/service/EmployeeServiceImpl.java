package jp.co.trainocate.enshu.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import jp.co.trainocate.enshu.entity.Employee;
import jp.co.trainocate.enshu.form.EmpForm;
import jp.co.trainocate.enshu.repository.EmpRepository;
import lombok.RequiredArgsConstructor;

/**
 * EmployeeServiceインタフェースの実装クラスです。
 * リポジトリ（EmpRepository）を利用し、従業員情報の操作を実現します。
 */
@Service
@RequiredArgsConstructor
public class EmployeeServiceImpl implements EmployeeService {

    /**
     * 従業員情報のデータ操作を行うリポジトリです。
     * コンストラクタインジェクションにより依存性を注入します。
     */
    @Autowired
    private final EmpRepository empRepo;
    
    /**
     * 指定されたIDに対応する従業員情報を取得します。
     * 該当する情報が存在しない場合はnullを返却します。
     * 
     * @param id 従業員ID
     * @return 該当するEmployeeオブジェクト、またはnull
     */
    @Override
    public Employee findEmployeeById(int id) {
        return empRepo.findById(id).orElse(null);
    }

    /**
     * 全従業員の情報を取得します。
     * 
     * @return 全従業員のリスト
     */
    @Override
    public List<Employee> findAllEmployees() {
        return empRepo.findAll();
    }

    
    /**
     * フォームから受け取った情報をもとに、従業員情報の新規登録または更新を行います。
     * フォームにIDが設定されている場合は、既存の従業員情報として更新処理を行い、
     * 設定されていない場合は新規登録として処理します。
     * 
     * @param empForm 従業員情報が格納されたフォーム
     */
    @Override
    public void saveEmployee(EmpForm empForm) {
        Employee emp = new Employee();
        // 更新処理の場合、フォームにIDが存在すればその値を設定します
        if (empForm.getId() != null) {
            emp.setId(empForm.getId());
        }
        emp.setName(empForm.getName());
        emp.setPassword(empForm.getPassword());
        emp.setSalary(empForm.getSalary());
        // リポジトリを利用して、従業員情報の新規登録または更新を実施します
        empRepo.save(emp);
    }

    /**
     * 指定されたIDの従業員情報を削除します。
     * 
     * @param id 削除対象の従業員ID
     */
    @Override
    public void deleteEmployee(int id) {
        empRepo.deleteById(id);
    }
}
