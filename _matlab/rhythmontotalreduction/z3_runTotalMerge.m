allFolders = dir('.\\measures');

for j = 1:length(allFolders)
    
    if allFolders(j).name(1) ~= '.'
        
        fprintf('Folder: %s\n', allFolders(j).name);
        
        foldName = allFolders(j).name;
        
        list = dir(sprintf('.\\measures\\%s\\*.txt',foldName));
        
        for i = 1:length(list)
            mergeTotalRedMeasure(foldName, list(i).name);
        end
        
    end
    
end