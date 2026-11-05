package jp.co.trainocate.enshu.service;

import java.util.List;

import jp.co.trainocate.enshu.entity.Employee;
import jp.co.trainocate.enshu.form.EmpForm;

/**
 * 従業員情報の操作（取得、登録、更新、削除）を定義するサービスインタフェースです。
 */
public interface EmployeeService {

    /**
     * 指定されたIDに対応する従業員情報を取得します。
     * @param id 従業員ID
     * @return 該当する従業員情報。該当しない場合はnullを返却します。
     */
    Employee findEmployeeById(int id);
    
    /**
     * 全従業員の情報を取得します。
     * @return 全従業員のリスト
     */
    List<Employee> findAllEmployees();
    
    /**
     * 指定された給与額と一致する従業員情報を取得します。
     * @param salary 給与額
     * @return 給与が一致する従業員のリスト
     */
    List<Employee> findEmployeesBySalary(int salary);
    
    /**
     * 指定された名前（部分一致）に該当する従業員情報を取得します。
     * @param name 検索対象の名前
     * @return 部分一致する従業員のリスト
     */
    List<Employee> findEmployeesByName(String name);
    
    /**
     * 従業員情報を新規登録または更新します。
     * @param empForm 従業員情報が格納されたフォーム
     */
    Employee saveEmployee(EmpForm empForm);
    
    /**
     * 指定されたIDの従業員情報を削除します。
     * @param id 削除対象の従業員ID
     */
    void deleteEmployee(int id);
}

